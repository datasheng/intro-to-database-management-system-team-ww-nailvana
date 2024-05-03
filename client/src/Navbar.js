import { Link } from 'react-router-dom';

const Navbar = () => {
    return (
       <nav className="navbar">
        <h1>Nailvana</h1>
        <div className="links">
            <Link to="/">Home</Link>
            <Link to="/appointments">Appointments</Link>
            <Link to="/schedule">Schedule</Link>
            <Link to="/signup" style={{
                color: "white",
                backgroundColor: '#6666cc',
                borderRadius: '8px'
            }}>Login</Link>
        </div>
       </nav> 
    );
}
 
export default Navbar;