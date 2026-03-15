import en from './en.json';
import ko from './ko.json';

export type Lang = 'en' | 'ko';
export const languages: Record<Lang, string> = { en: 'EN', ko: 'KO' };
export const defaultLang: Lang = 'en';

const translations = { en, ko } as const;

export function t(lang: Lang) {
  return translations[lang];
}
