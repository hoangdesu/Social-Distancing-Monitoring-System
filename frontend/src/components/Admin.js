import React, { useState, useEffect, useCallback } from 'react';

import LoginForm from './LoginForm';
import Dashboard from './Dashboard';

const Admin = () => {
    const [isLoggedIn, setLogin] = useState(false);
    const [activeAccount, setActiveAccount] = useState('');

    const setLocalStorage = useCallback(() => {
        const activeUser = JSON.parse(localStorage.getItem('activeUser'));
        if (activeUser !== 'admin')
            localStorage.setItem('activeUser', JSON.stringify(activeAccount));
        else setLogin(true);
        console.log(activeUser);
    }, [activeAccount]);

    useEffect(() => {
        document.title = "Kiti - Admin's section"
     }, []);

    useEffect(() => {
        setLocalStorage();
    }, [setLocalStorage]);
    
    

    const getAccount = (account) => {
        // console.log('ACTIVE ACCOUNT', data);
        setActiveAccount(account);
    };

    return (
        <div>
            {!isLoggedIn ? (
                <LoginForm setLogin={setLogin} getAccount={getAccount} />
            ) : (
                <Dashboard setLogin={setLogin} />
            )}
        </div>
    );
};

export default Admin;
