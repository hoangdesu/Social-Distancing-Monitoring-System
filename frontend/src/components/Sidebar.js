import React, { useState } from 'react';

import { NavLink, useLocation } from 'react-router-dom';
import styled from 'styled-components';

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
    margin: 40px 0;
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
        activeItem: false
    },
    {
        title: 'Analytics',
        route: '/analytics',
        icon: analyticsIcon,
        iconActive: analyticsIconActive,
        activeItem: false
    },
    {
        title: 'About',
        route: '/about',
        icon: aboutIcon,
        iconActive: aboutIconActive,
        activeItem: false
    },
    {
        title: 'Settings',
        route: '/settings',
        icon: settingsIcon,
        iconActive: settingsIconActive,
        activeItem: false
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
    
    
    // TODO: fix bug icon lag behind!!
    const setActive = () => {
        setMenuItems(prev => {
            const newList = prev.map(item => {
                if (item.route === location.pathname) {
                    item.activeItem = true;
                } else {
                    item.activeItem = false;
                }
                console.log(item.title, item.activeItem)
                
                return item;
            })
            return [...newList];
        })
    }

    return (
        <Container>
            <h1>Sidebar</h1>
            <h2>Logo here</h2>
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
                            <img src={item.activeItem ? item.iconActive : item.icon} alt="icon" />
                            <span>{item.title}</span>
                        </NavLink>
                    );
                })}
            </MenuList>
        </Container>
    );
};

export default Sidebar;