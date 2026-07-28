import React from 'react';
import { motion, HTMLMotionProps } from 'framer-motion';
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

interface GlassPanelProps extends HTMLMotionProps<'div'> {
  children: React.ReactNode;
  className?: string;
  intensity?: 'light' | 'medium' | 'heavy';
  elevated?: boolean;
}

export const GlassPanel: React.FC<GlassPanelProps> = ({
  children,
  className,
  intensity = 'medium',
  elevated = true,
  ...props
}) => {
  const blurMap = {
    light: 'backdrop-blur-md bg-slate-900/60',
    medium: 'backdrop-blur-2xl bg-slate-950/80',
    heavy: 'backdrop-blur-3xl bg-slate-950/92',
  };

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.98 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.98 }}
      transition={{ duration: 0.15, ease: [0.16, 1, 0.3, 1] }}
      className={twMerge(
        clsx(
          'relative overflow-hidden rounded-2xl border border-white/10 text-slate-100 shadow-2xl',
          blurMap[intensity],
          elevated && 'shadow-[0_20px_50px_rgba(0,0,0,0.6)]',
          className
        )
      )}
      {...props}
    >
      {children}
    </motion.div>
  );
};
