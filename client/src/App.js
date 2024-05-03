import React, { useState,  useEffect} from 'react';
import logo from './logo.svg';
import './App.css';
import FullCalendar from '@fullcalendar/react';
import dayGridPlugin from '@fullcalendar/daygrid'; // a plugin!
import Chat from './Chat';

function App() {
  // Create a state variable for events
  const [events, setEvents] = useState([]);

  useEffect(() => {
    console.log('Events updated:', events);
  }, [events]);

  return (
    <div style={{ display: 'flex', flexDirection: 'row' }}>
      <div style={{ flex: 1 }}>
        <FullCalendar
          plugins={[ dayGridPlugin ]}
          initialView={'dayGridWeek'}
          headerToolbar={{
            left: 'prev,next',
            center: 'title',
            right: 'dayGridWeek,dayGridDay' // user can switch between the two
          }}
          events={events} // Use the state variable here
        />
      </div>
      <div style={{ flex: 1 }}>
        <Chat events={events} setEvents={setEvents} /> 
      </div>
    </div>
  );
}

export default App;
