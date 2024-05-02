import { Link } from "react-router-dom";

const AppointmentList = ({ appointments, title /*, handleCancel*/ }) => {
// const appointments = props.appointments;
// const title = props.title;


    return (
        <div className="appointment-list">
            <h2> { title }</h2>
            {appointments.map((appointment) =>(
                <div className="appointment-preview" key={appointment.id}>
                    <Link to={`/appointments/${appointment.id}`}>
                        {}
                        <h2>{ appointment.customer }</h2>   
                        <p>Taken services with { appointment.provider }</p>  
                        {/* <button onClick={() => handleCancel(appointment.id)}>Canccel Appointment</button>*/}
                    </Link>
                </div>    
            ))}
        </div>
    );
}
 
export default AppointmentList;