import { useState } from "react";
import React from "react";
import { useHistory } from "react-router-dom";

const Schedule = () => {
    const [customer, setCustomer] = useState('');
    const [provider, setProvider] = useState('jennifer');
    const [date, setDate] = useState('0000-00-00');
    const [time, setTime] = useState('00:00');
    const [isPending, setIsPendig] = useState(false);
    const history = useHistory();
    

    const option = [
        {technician:"jennifer", technicianId: 1},
        {technician:"julia", technicianId: 2},
        {technician:"ana", technicianId: 3}
    ]

    const handleSubmit = (e) => {
        e.preventDefault();
        const appointment = { customer, provider, date, time};

        setIsPendig(true);
        
        fetch('http://localhost:8000/appointments', {
            method: 'POST',
            headers:{ "Content-Type": "application/json" },
            body: JSON.stringify(appointment)
        }).then(() => {
            console.log('new appointment added');
            setIsPendig(false);
            //history.go(-1); //goes to the previous step
            history.push('/');
        })
    }

    return (
        <div className="schedule">
            <h2>Schedule a New Appointment</h2>
            <form onSubmit={handleSubmit}>
            <label>Your Name:</label>
            <input 
                type="text"
                id="customerName"
                required
                value={customer}
                onChange={(e) =>  setCustomer(e.target.value)}                
            />

            <label>Technician Chosen:</label>
            <select
                value={ provider }
                onChange={(e) => setProvider(e.target.value)}
            >
                {option.map(option => (
                    <option value={option.value}>
                        {option.technician}
                    </option>
                ))}
                
            </select>

            <label>Chosen date:</label>
            <input
                type="date"
                id="date"
                min="2024-05-07"
                max="2024-05-14"
                required
                value={ date }
                onChange={(e) => setDate(e.target.value)}
            />

            <label>Chosen time:<small> Office hour from 9am to 8pm</small></label>
            <input
                type="time"
                id="time"
                min="09:00"
                max="20:00"
                required
                value={ time }
                onChange={(e) => setTime(e.target.value)}
            />

            <br></br>

            { !isPending && <button>Make Appointment</button>}
            { isPending && <button disabled>Adding appointment...</button>}

            </form>
        </div>
    );
}
 
export default Schedule;