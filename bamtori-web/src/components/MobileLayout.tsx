import React from 'react';

export default function MobileLayout({ children, className = "" }: { children: React.ReactNode; className?: string }) {
  return (
    <main className={`max-w-md mx-auto min-h-dvh relative z-10 flex flex-col ${className}`}>
      {children}
    </main>
  );
}
