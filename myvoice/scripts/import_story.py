
import os
import re
import asyncio
import sys
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, delete

from app.config import get_settings
from app.models.curriculum import CurriculumUnit, Activity

settings = get_settings()

async def import_story(file_path: str):
    if not os.path.exists(file_path):
        print(f"Error: File found at {file_path}")
        return

    print(f"Reading {file_path}...")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Parse Metadata
    title_match = re.search(r'^# \[(.*?)\] (.*)', content, re.MULTILINE)
    if not title_match:
        print("Error: Title not found. Check format '# [Vol] Title'")
        return
    
    vol_info = title_match.group(1)
    title_text = title_match.group(2).strip()
    
    unit_id = os.path.basename(file_path).replace('.md', '').lower()
    
    theme_match = re.search(r'\*\*테마:\*\* (.*)', content)
    concept_match = re.search(r'\*\*핵심 컨셉:\*\* (.*)', content)
    
    description = ""
    if theme_match: description += f"Theme: {theme_match.group(1)}\n"
    if concept_match: description += f"Concept: {concept_match.group(1)}\n"

    print(f"Found Story: {title_text} (ID: {unit_id})")

    # 2. Parse Pages
    page_pattern = re.compile(r'## \*\*\[Page (\d+): (.*?)\]\*\*(.*?)(?=##|\Z)', re.DOTALL)
    pages = page_pattern.findall(content)
    
    activities = []
    
    for page_num, page_title, page_content in pages:
        activity_id = f"{unit_id}_p{page_num}"
        
        situation_match = re.search(r'\*\s+\*\*상황:\*\* (.*?)\n', page_content)
        content_match = re.search(r'\*\s+\*\*내용:\*\*\s*\n(.*?)(?=\*\s+\*\*Mission)', page_content, re.DOTALL)
        mission_match = re.search(r'\*\s+\*\*Mission:\*\* "(.*?)"', page_content)
        subtitle_match = re.search(r'\*\s+\*\*부제:\*\* (.*?)\n', page_content)
        image_guide_match = re.search(r'\*\s+\*\*그림 가이드:\*\*[:\s]*\n(.*?)(?=\n\*\s+\*\*Mission)', page_content, re.DOTALL)
        
        situation = situation_match.group(1).strip() if situation_match else ""
        story_text = content_match.group(1).strip() if content_match else ""
        key_expr = mission_match.group(1).strip() if mission_match else None
        subtitle = subtitle_match.group(1).strip() if subtitle_match else ""
        
        image_prompt = ""
        if image_guide_match:
            raw_guide = image_guide_match.group(1)
            image_prompt = re.sub(r'\s*\*\s+', ' ', raw_guide).strip()
        else:
            clean_text = re.sub(r'[\r\n]+', ' ', story_text)[:150]
            image_prompt = f"Scene Description: {situation}. Details: {clean_text}"
        
        act_type = "narrative"
        if int(page_num) == 1:
            act_type = "intro"
        elif key_expr:
            act_type = "guided_conversation" 
        
        # Fallback for narrator script (e.g. Cover Page)
        narrator_script = story_text
        if not narrator_script and subtitle:
            narrator_script = subtitle
        elif not narrator_script and int(page_num) == 1:
            narrator_script = f"Story: {title_text}"
        
        activity = Activity(
            activity_id=activity_id,
            curriculum_unit_id=unit_id,
            name=f"Page {page_num}: {page_title.strip()}",
            activity_type=act_type,
            intro_narrator_script=narrator_script,
            key_expression=key_expr,
            story_content=f"Situation: {situation}\n\n{story_text}\n\nSubtitle: {subtitle}",
            image_prompt=image_prompt,
            estimated_duration_minutes=3
        )
        activities.append(activity)
        print(f"  - Page {page_num}: {page_title.strip()} (Script Len: {len(narrator_script)}, Image: {'Yes' if image_prompt else 'No'})")

    # 3. DB Ops
    engine = create_async_engine(settings.database_url)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as db:
        db_unit = await db.get(CurriculumUnit, unit_id)
        if db_unit:
            print("Updating existing unit...")
            db_unit.title = title_text
            db_unit.description = description
        else:
            print("Creating new unit...")
            db_unit = CurriculumUnit(
                curriculum_unit_id=unit_id,
                title=title_text,
                description=description,
                difficulty_level=1,
                week=1,
                language_mode="mixed"
            )
            db.add(db_unit)
        
        await db.execute(delete(Activity).where(Activity.curriculum_unit_id == unit_id))
        db.add_all(activities)
        await db.commit()
    
    print("Import successful!")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/import_story.py <path_to_md>")
        sys.exit(1)
    
    path = sys.argv[1]
    asyncio.run(import_story(path))
