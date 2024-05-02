import { useHistory, useParams } from "react-router-dom";
import useFetch from "./useFetch";

const AppointmentDetails = () => {
    const { id } = useParams();
    const { data: appointment, error, isPendding } = useFetch('http://localhost:8000/appointments/' + id);
    const history = useHistory();
   
    const handleClick= () => {
        fetch('http://localhost:8000/appointments/' + appointment.id, {
            method: 'DELETE'
        }).then(() =>{
            history.push('/');
        })
    }

    return (
        <div className="appointment-details">
            { isPendding && <div>Loading...</div> }
            { error && <div>{ error }</div> }
            { appointment && (
                <article>
                    <h2>Appointment Detail - { id }</h2>
                    <p>Customer: { appointment.customer }</p>
                    <div>Technition: { appointment.provider }</div>
                    <div>Date: { appointment.date }</div>
                    <div>Time: { appointment.time }</div>
                    <button onClick={handleClick}>Cancel Appointment</button> 
                </article>
            )}
        </div>
    );
}
 
export default AppointmentDetails;