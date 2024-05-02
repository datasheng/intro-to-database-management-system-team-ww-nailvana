import { useParams } from "react-router-dom";
import useFetch from "./useFetch";

const AppointmentDetails = () => {
    const { id } = useParams();
    const { data: appointments, error, isPendding } = useFetch('http://localhost:8000/appointments/' + id);
    
    return (
        <div className="appointment-details">
            { isPendding && <div>Loading...</div> }
            { error && <div>{ error }</div> }
            { appointments && (
                <article>
                    <h2>Appointment Detail - { id }</h2>
                    <p>Customer: { appointments.customer }</p>
                    <div>Service: { appointments.body }</div>
                    <div>Technition: { appointments.provider }</div>
                </article>
            )}
        </div>
    );
}
 
export default AppointmentDetails;