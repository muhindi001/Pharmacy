import React from "react";

const StatCard = ({
  title,
  value,
  icon,
  color = "bg-blue-500",
  subtitle = "",
}) => {
  return (
    <div className="bg-white rounded-xl shadow-md p-5 hover:shadow-lg transition-all duration-300">
      <div className="flex justify-between items-center">
        <div>
          <h4 className="text-sm text-gray-500">{title}</h4>

          <h2 className="text-3xl font-bold text-gray-800 mt-2">
            {value}
          </h2>

          {subtitle && (
            <p className="text-xs text-gray-500 mt-2">
              {subtitle}
            </p>
          )}
        </div>

        <div
          className={`w-14 h-14 rounded-full flex items-center justify-center text-white ${color}`}
        >
          {icon}
        </div>
      </div>
    </div>
  );
};

export default StatCard;