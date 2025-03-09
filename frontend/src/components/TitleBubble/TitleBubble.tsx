import React from "react";

interface TitleBubbleProps {
  text: string;
}

const TitleBubble: React.FC<TitleBubbleProps> = ({ text }) => {
  return (
    <div className="inline-flex items-center px-4 py-1 bg-green-400 rounded-full border-2 border-black shadow-lg relative">
      <span className="text-black font-bold tracking-widest">{text}</span>
      <div className="absolute -top-1 left-0 right-0 h-1 border-t-2 border-dashed border-black"></div>
    </div>
  );
};

export default TitleBubble;
