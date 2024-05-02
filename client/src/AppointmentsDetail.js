import { useHistory } from "react-router";
import AppointmentList from "./AppointmentList";
import useFetch from "./useFetch";

const AppointmentsDetail = () => {
    const { data: appointments, isPending, error } = useFetch('http://localhost:8000/appointments');
    //const [name, setName] = useState('jennifer');
    
    // const handleCancel = (id) => {
    //     const newAppointments = appointments.filter(appointment => appointment.id !== id);
    //     setAppointments(newAppointments);
    // }

    

    return (
        <div className="appointments-detail">
            { error && <div>{ error }</div>}
            { isPending && <div>Loading...</div> }
            {appointments && 
                <AppointmentList appointments={appointments} title="All Appointments Taken" /*handleCancel={handleCancel}*/ />
}   
            {/* <AppointmentList appointments={appointments.filter((appointment) => appointment.provider === 'jennifer')} title="Jennifer's Appointments" /> */}
        </div>
    );
}
 
export default AppointmentsDetail;