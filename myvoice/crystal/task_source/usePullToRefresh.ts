import { useEffect, useRef, useState } from 'react';

interface UsePullToRefreshOptions {
  onRefresh: () => Promise<void>;
  threshold?: number;
  resistance?: number;
}

export function usePullToRefresh({
  onRefresh,
  threshold = 80,
  resistance = 2.5,
}: UsePullToRefreshOptions) {
  const [isPulling, setIsPulling] = useState(false);
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [pullDistance, setPullDistance] = useState(0);
  const startY = useRef(0);
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    let touchStartY = 0;
    let scrollTop = 0;

    const handleTouchStart = (e: TouchEvent) => {
      if (isRefreshing) return;
      
      scrollTop = container.scrollTop;
      touchStartY = e.touches[0].clientY;
      startY.current = touchStartY;
    };

    const handleTouchMove = (e: TouchEvent) => {
      if (isRefreshing) return;
      
      const currentY = e.touches[0].clientY;
      const deltaY = currentY - touchStartY;

      // Only trigger pull-to-refresh when at the top of the scroll
      if (scrollTop === 0 && deltaY > 0) {
        setIsPulling(true);
        const distance = Math.min(deltaY / resistance, threshold * 1.5);
        setPullDistance(distance);
        
        // Prevent default scroll behavior when pulling
        if (deltaY > 10) {
          e.preventDefault();
        }
      }
    };

    const handleTouchEnd = async () => {
      if (isRefreshing) return;
      
      setIsPulling(false);

      if (pullDistance >= threshold) {
        setIsRefreshing(true);
        setPullDistance(threshold);
        
        try {
          await onRefresh();
        } finally {
          setTimeout(() => {
            setIsRefreshing(false);
            setPullDistance(0);
          }, 500);
        }
      } else {
        setPullDistance(0);
      }
    };

    container.addEventListener('touchstart', handleTouchStart, { passive: true });
    container.addEventListener('touchmove', handleTouchMove, { passive: false });
    container.addEventListener('touchend', handleTouchEnd, { passive: true });

    return () => {
      container.removeEventListener('touchstart', handleTouchStart);
      container.removeEventListener('touchmove', handleTouchMove);
      container.removeEventListener('touchend', handleTouchEnd);
    };
  }, [isRefreshing, pullDistance, threshold, resistance, onRefresh]);

  return {
    containerRef,
    isPulling,
    isRefreshing,
    pullDistance,
    threshold,
  };
}
