import React from 'react';
import classes from './MainNav.module.css';
import { NavLink } from 'react-router-dom';

const MainNav = () => {

    return (

        <nav className={classes.MainNav}>
            <ul>
                <li>
                    <NavLink to="/actors" activeClassName={classes.active}>Actors</NavLink>
                </li>
                <li>
                    <NavLink to="/movies" activeClassName={classes.active} >Movies</NavLink>
                </li>
            </ul>
        </nav>

    );
};

export default MainNav;