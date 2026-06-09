import React from 'react';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost' | 'ai';
  size?: 'sm' | 'md' | 'lg';
  icon?: string;
  shimmer?: boolean;
}

export const Button: React.FC<ButtonProps> = ({
  children,
  variant = 'primary',
  size = 'md',
  icon,
  shimmer = false,
  className = '',
  ...props
}) => {
  const baseStyles = 'inline-flex items-center justify-center font-bold transition-all active:scale-[0.98] select-none';
  
  const variants = {
    primary: 'bg-primary text-on-primary hover:opacity-90 active:opacity-80 rounded-xl shadow-md',
    secondary: 'bg-secondary text-on-secondary hover:opacity-90 active:opacity-80 rounded-xl',
    outline: 'border border-outline text-primary hover:bg-surface-container-low rounded-xl',
    ghost: 'text-on-surface-variant hover:bg-surface-container-high rounded-xl',
    ai: 'bg-on-tertiary-container text-white ai-shimmer hover:opacity-90 rounded-xl shadow-md',
  };

  const sizes = {
    sm: 'px-3 py-1.5 text-xs',
    md: 'px-5 py-2.5 text-sm',
    lg: 'px-8 py-4 text-base',
  };

  const shimmerClass = shimmer ? 'shimmer-btn' : '';

  return (
    <button
      className={`${baseStyles} ${variants[variant]} ${sizes[size]} ${shimmerClass} ${className}`}
      {...props}
    >
      {icon && (
        <span className="material-symbols-outlined mr-2 text-[18px]">
          {icon}
        </span>
      )}
      {children}
    </button>
  );
};

export default Button;
