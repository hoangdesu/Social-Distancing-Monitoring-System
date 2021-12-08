import React, { useState, useEffect } from 'react';

import { NavLink, useLocation } from 'react-router-dom';
import styled from 'styled-components';

import rpg_logo from '../assets/logo/rpg_logo.png';
import dashboardIcon from '../assets/icons/dashboard.svg';
import dashboardIconActive from '../assets/icons/dashboardActive.svg';
import liveIcon from '../assets/icons/live.svg';
import liveIconActive from '../assets/icons/liveActive.svg';
import settingsIcon from '../assets/icons/settings.svg';
import settingsIconActive from '../assets/icons/settingsActive.svg';
import analyticsIcon from '../assets/icons/analytics.svg';
import analyticsIconActive from '../assets/icons/analyticsActive.svg';
import aboutIcon from '../assets/icons/about.svg';
import aboutIconActive from '../assets/icons/aboutActive.svg';
import back from '../assets/icons/back.svg';

import SidebarCSS from './Sidebar.module.css';

const Container = styled.div`
    // position: fixed;
    background: #081a51;
    width: 15vw;
    min-width: 180px;
    height: 100vh;
    display: flex;
    flex-direction: column;
    font-family: 'SVN-Gilroy Medium';
    color: #ccd2e3;
    // padding: 20px;
    // box-shadow: 1px 0px 2px 1px #aaa;
    // z-index: 1;
`;

const MenuList = styled.ul`
    margin: 10px 0;
    list-style: none;
    display: flex;
    flex-direction: column;
`;



const menuItemsOriginal = [
    {
        title: 'Dashboard',
        route: '/',
        icon: dashboardIcon,
        iconActive: dashboardIconActive,
        activeItem: true,
    },
    {
        title: 'Live',
        route: '/live',
        icon: liveIcon,
        iconActive: liveIconActive,
        activeItem: false,
    },
    {
        title: 'Analytics',
        route: '/analytics',
        icon: analyticsIcon,
        iconActive: analyticsIconActive,
        activeItem: false,
    },
    {
        title: 'About',
        route: '/about',
        icon: aboutIcon,
        iconActive: aboutIconActive,
        activeItem: false,
    },
    {
        title: 'Settings',
        route: '/settings',
        icon: settingsIcon,
        iconActive: settingsIconActive,
        activeItem: false,
    },
];

const Sidebar = (props) => {
    const location = useLocation();
    const [menuItems, setMenuItems] = useState(menuItemsOriginal);

    props.getTitle(location.pathname);

    // const navlinkActiveHandler = (match, location) => {
    //     console.log(location.pathname)
    //     if (location.pathname === item.route) console.log('con')
    // }

    const setActive = () => {
        setMenuItems((prev) => {
            const newList = prev.map((item) => {
                if (item.route === location.pathname) {
                    item.activeItem = true;
                    // console.log(item.title)
                } else {
                    item.activeItem = false;
                }
                // console.log(item.title, item.activeItem)
                return item;
            });
            return [...newList];
        });
    };

    // Also change active icon. BUG FIXED!
    useEffect(() => {
        setMenuItems((prev) => {
            const newList = prev.map((item) => {
                if (item.route === location.pathname) {
                    item.activeItem = true;
                    // console.log(item.title)
                } else {
                    item.activeItem = false;
                }
                return item;
            });
            return [...newList];
        });
    }, [location.pathname]);

    //
    const logoutHandler = () => {
        // const activeUser = JSON.parse(localStorage.getItem("activeUser"));
        localStorage.removeItem('activeUser');
        setTimeout(() => {
            props.setLogin(false);
        }, 500);
    };

    return (
        <Container>
            <div
                style={{
                    padding: '10px',
                    display: 'flex',
                    // border: '1px solid red',
                    alignItems: 'center',
                    justifyContent: 'center',
                }}
            >
                <img src={rpg_logo} alt="" width="60%" />
            </div>
            <MenuList>
                <label>MAIN MENU</label>
                {menuItems.map((item, index) => {
                    return (
                        <NavLink
                            key={index}
                            exact
                            to={item.route}
                            onClick={setActive}
                            className={SidebarCSS.navlink}
                            activeClassName={SidebarCSS.active}
                        >
                            <img
                                src={
                                    item.activeItem
                                        ? item.iconActive
                                        : item.icon
                                }
                                alt="icon"
                            />
                            <span>{item.title}</span>
                        </NavLink>
                    );
                })}
            </MenuList>
            <button
                className={SidebarCSS.btnLogout}
                onClick={logoutHandler}
            >
                <img
                    src={back}
                    alt=""
                    width="20px"
                    style={{ marginRight: '10px' }}
                />
                Log out
            </button>
        </Container>
    );
};

export default Sidebar;
