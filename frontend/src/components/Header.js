import React from 'react';
import classes from './Header.module.css'
import { useAuth0 } from '@auth0/auth0-react';
import BtnLoginLogout from './BtnLoginLogout';

const Header = () => {
    const { user, isAuthenticated, isLoading } = useAuth0();

    if (isLoading) {
        return (<div>Loading</div>);

    } else {
        var showInfo = isAuthenticated && (<React.Fragment>
            <div style={{ float: "right" }}>

                <ul className={classes.ulInfo}>
                    <li>
                        Name:{user.name}
                    </li>
                    <li>
                        Access:
                    </li>
                </ul>
            </div>

            <li style={{ float: "right" }}>
                <img className={classes.Profile} alt={user.name} src={user.picture}></img>
            </li>
        </React.Fragment>)

        return (
            <header className={classes.Header}>
                <ul>
                    <li>
                        Casting Agencies
                    </li>
                    <li style={{ float: "right" }}>
                        <BtnLoginLogout/>
                    </li>
                    {showInfo}
                </ul>
            </header>
        );
    }
}
export default Header;