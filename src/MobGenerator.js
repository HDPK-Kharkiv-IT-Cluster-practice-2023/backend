import React, { useState, useEffect } from 'react';
import './MobGenerator.css';
import MobList from './MobList';
import MobStats from './MobStats';
import LevelButtons from './LevelButtons';

function MobGenerator() {
  const [mobs, setMobs] = useState([]);
  const [mobLevel, setMobLevel] = useState(1);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(`http://localhost:5000/?level=${mobLevel}`);
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data = await response.json();
        setMobs(data);
      } catch (error) {
        console.error('Ошибка при получении данных:', error);
      }
    };

    fetchData();
  }, [mobLevel]);

  const updateMobStats = (level) => {
    const newAttack = Math.max(2 + level, 0);
    const newHealth = Math.max(20 + level * 5, 0);
    const newArmor = Math.max(1 + level, 0);
    return { attack: newAttack, health: newHealth, armor: newArmor };
  };

  const handleLevelChange = (newLevel) => {
    const updatedLevel = Math.max(newLevel, 1);
    const prevStats = updateMobStats(mobLevel);
    const newStats = updateMobStats(updatedLevel);

    const updatedMobs = mobs.map((mob) => ({
      ...mob,
      attack: mob.attack + (newStats.attack - prevStats.attack),
      health: mob.health + (newStats.health - prevStats.health),
      armor: mob.armor + (newStats.armor - prevStats.armor),
    }));

    setMobLevel(updatedLevel);
    setMobs(updatedMobs);
  };

  return (
    <div className="mob-generator-container">
      <h1>Информация о мобах</h1>
      <MobList mobs={mobs} />
      <MobStats mobs={mobs} />
      <LevelButtons
        mobLevel={mobLevel}
        onLevelIncrease={() => handleLevelChange(mobLevel + 1)}
        onLevelDecrease={() => handleLevelChange(mobLevel - 1)}
      />
    </div>
  );
}

export default MobGenerator;
