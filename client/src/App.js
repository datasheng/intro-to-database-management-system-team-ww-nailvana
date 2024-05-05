import Navbar from './Navbar';
import Home from './Home';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Schedule from './Schedule';
import AppointmentDetails from './AppointmentDetails';
import AppointmentsL from './AppointmentsL';
import SignUp from './SignUp';

function App() {

  return (
    <Router>
      <div className="App">
        <Navbar />
        <div className="content">
          <Switch>
            <Route exact path="/">
              <Home />
            </Route>
            <Route exact path="/appointments">
              <AppointmentsL />
            </Route>
            <Route exact path="/schedule">
              <Schedule />
            </Route>
            <Route exact path="/signup">
              <SignUp />
            </Route>
            <Route path="/appointments/:id">
              <AppointmentDetails />
            </Route>
          </Switch>
        </div>
      </div>
    </Router>
  );
}

export default App;
