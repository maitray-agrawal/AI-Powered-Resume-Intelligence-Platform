import React from 'react';

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  hoverEffect?: boolean;
}

export const Card: React.FC<CardProps> = ({
  children,
  hoverEffect = true,
  className = '',
  ...props
}) => {
  const hoverStyles = hoverEffect ? 'hover:shadow-lg transition-shadow duration-300' : '';
  return (
    <div
      className={`bg-white rounded-2xl border border-outline-variant p-6 ${hoverStyles} ${className}`}
      {...props}
    >
      {children}
    </div>
  );
};

export default Card;
