import React from 'react';
import { useAuth0 } from '@auth0/auth0-react';
import MainNav from './MainNav';
import { Switch, Route, Redirect } from 'react-router-dom';

const Main = () => {
    const { isAuthenticated } = useAuth0();

    return !isAuthenticated && (
        <main style={{ color: 'white', display: 'flex', margin: "40px 40px" }}>
            <div style={{ flex: "10%" }}>
                <MainNav></MainNav>
            </div>
            <div style={{ flex: "90%" }}>
                <Switch>
                    <Route path="/actors"  >

                    </Route>
                    <Route path="/movies">

                    </Route>
                    <Redirect to="/"/>
                </Switch>

            </div>
        </main>
    );
}

export default Main;