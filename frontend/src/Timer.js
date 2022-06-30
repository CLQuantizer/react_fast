import React from 'react';
import { useTimer } from 'react-timer-hook';

function MyTimer({expiryTimestamp, setIsLoggedIn}) {
  const {
    seconds,
    minutes,
    hours,
    days,
    isRunning,
    start,
    pause,
    resume,
    restart,
  } = useTimer({ expiryTimestamp, 
    onExpire: () => {
        console.warn('onExpire called');
        setIsLoggedIn(false);
        localStorage.removeItem('accessToken');
        localStorage.removeItem('expiration');
      }
  });

  return (
    <div style={{textAlign: 'center'}}>

      <p>it will expire in </p>
      <div style={{fontSize: '100px'}}>
        <span>{hours}</span>:<span>{minutes}</span>:<span>{seconds}</span>
      </div>
      {/* <p>{isRunning ? 'Running' : 'Not running'}</p> */}
      {/* <button onClick={start}>Start</button>
      <button onClick={pause}>Pause</button>
      <button onClick={resume}>Resume</button>
      <button onClick={() => {
        // Restarts to 5 minutes timer
        const time = new Date();
        time.setSeconds(time.getSeconds() + 300);
        restart(time)
      }}>Restart</button> */}
    </div>
  );
}

export default MyTimer;