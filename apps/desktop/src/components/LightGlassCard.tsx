import React from 'react';
import { motion, HTMLMotionProps } from 'framer-motion';
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

interface LightGlassCardProps extends HTMLMotionProps<'div'> {
  children: React.ReactNode;
  className?: string;
  elevated?: boolean;
}

export const LightGlassCard: React.FC<LightGlassCardProps> = ({
  children,
  className,
  elevated = true,
  ...props
}) => {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.98 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.98 }}
      transition={{ duration: 0.16, ease: [0.16, 1, 0.3, 1] }}
      className={twMerge(
        clsx(
          'relative overflow-hidden rounded-2xl zero-light-glass text-slate-900',
          elevated && 'shadow-[0_25px_60px_-15px_rgba(0,0,0,0.12)]',
          className
        )
      )}
      {...props}
    >
      {children}
    </motion.div>
  );
};
