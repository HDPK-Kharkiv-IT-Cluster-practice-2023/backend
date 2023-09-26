import React from 'react';

function LevelButtons({ mobLevel, onLevelIncrease, onLevelDecrease }) {
  return (
    <div className="level-buttons">
      <h2>Уровень моба: {mobLevel}</h2>
      <button onClick={onLevelIncrease}>Увеличить уровень</button>
      <button onClick={onLevelDecrease}>Уменьшить уровень</button>
    </div>
  );
}

export default LevelButtons;
