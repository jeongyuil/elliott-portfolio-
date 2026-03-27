"use client";

import React, { useEffect, useState } from 'react';

export default function StarryBackground() {
  const [stars, setStars] = useState<{ id: number; top: string; left: string; size: number; delay: string }[]>([]);

  useEffect(() => {
    // Generate random stars on client-side only to avoid hydration mismatch
    const newStars = Array.from({ length: 50 }).map((_, i) => ({
      id: i,
      top: `${Math.random() * 100}%`,
      left: `${Math.random() * 100}%`,
      size: Math.random() * 3 + 1, // 1px to 4px
      delay: `${Math.random() * 3}s`,
    }));
    setStars(newStars);
  }, []);

  return (
    <div className="fixed inset-0 z-0 overflow-hidden pointer-events-none">
      <div className="absolute inset-0 bg-gradient-to-b from-[--color-bamtori-dark] to-[#1a1f2e] opacity-80" />
      {stars.map((star) => (
        <div
          key={star.id}
          className="absolute rounded-full bg-white animate-twinkle"
          style={{
            top: star.top,
            left: star.left,
            width: `${star.size}px`,
            height: `${star.size}px`,
            animationDelay: star.delay,
            opacity: Math.random() * 0.7 + 0.3,
          }}
        />
      ))}
    </div>
  );
}
