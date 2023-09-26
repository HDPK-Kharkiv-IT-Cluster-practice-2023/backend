import React from 'react';

function MobStats({ mobs }) {
  return (
    <ul className="mob-stats">
      {mobs.map((mob, index) => (
        <li key={index}>
          <p>Health: {mob.health}</p>
          <p>Armor: {mob.armor}</p>
          <p>Attack: {mob.attack}</p>
          <p>Luck: {mob.luck}</p>
        </li>
      ))}
    </ul>
  );
}

export default MobStats;
