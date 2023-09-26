import React from 'react';

function MobList({ mobs }) {
  return (
    <ul className="mob-list">
      {mobs.map((mob, index) => (
        <li key={index}>
          <p>Name: {mob.name}</p>
        </li>
      ))}
    </ul>
  );
}

export default MobList;
