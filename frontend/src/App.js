import React, { useState, useEffect, useCallback } from 'react';

import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import styled from 'styled-components';

import Sidebar from './components/Sidebar';
import NavBar from './components/NavBar';
import Dashboard from './components/Dashboard';
import Live from './components/Live';
import About from './components/About';
import LoginForm from './components/LoginForm';

const AppContainer = styled.div`
    display: flex;
    flex-direction: row;
`;

const Content = styled.div`
    background-color: #F8F9Ff;
    // background-color: #edeff7;
    width: 100%;
    overflow: scroll;
    // z-index: 10;
    // padding: 20px;
`;

function App() {
    const [title, setTitle] = useState('/');

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
        setLocalStorage();
    }, [setLocalStorage]);

    const getAccount = (account) => {
        // console.log('ACTIVE ACCOUNT', data);
        setActiveAccount(account);
    };

    const contentClickHandler = (val) => {
        setTitle(val);
    };

    return (
        <Router>
            {!isLoggedIn ? (
                <LoginForm setLogin={setLogin} getAccount={getAccount} />
            ) : (
                <AppContainer>
                    <Sidebar getTitle={contentClickHandler} setLogin={setLogin} />
                    <Content>
                        <NavBar title={title} />
                        <Switch>
                            <Route exact path="/">
                                <Dashboard />
                            </Route>
                            <Route exact path="/dashboard">
                                <Dashboard />
                            </Route>
                            <Route exact path="/live">
                                <Live />
                            </Route>
                            <Route exact path="/about">
                                <About />
                            </Route>
                        </Switch>
                    </Content>
                </AppContainer>
            )}
        </Router>
    );
}

export default App;
