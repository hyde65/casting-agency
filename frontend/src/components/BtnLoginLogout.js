import React from 'react';
import { useAuth0 } from '@auth0/auth0-react';
import classes from './BtnLoginLogout.module.css';

const BtnLoginLogout = (props) => {
    const { isAuthenticated, loginWithRedirect, logout } = useAuth0();

    if (!isAuthenticated) {
        return (
            <button className={classes.BtnLoginLogout} onClick={()=>loginWithRedirect()}>
                Sign In
            </button>
        )
    } else {
        return (
            <button className={classes.BtnLoginLogout} onClick={()=>logout()}>
                Logout
            </button>)
    }


}

export default BtnLoginLogout;