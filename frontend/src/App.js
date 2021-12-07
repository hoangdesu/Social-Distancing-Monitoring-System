import React, { useState } from 'react';

import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import styled from 'styled-components';

import Sidebar from './components/Sidebar';
import NavBar from './components/NavBar';
import Dashboard from './components/Dashboard';
import Live from './components/Live';
import About from './components/About';

const AppContainer = styled.div`
    display: flex;
    flex-direction: row;
`;

const Content = styled.div`
    background-color: #F8F9FF;
    width: 100%;
    overflow: scroll;
                // CAM6
    // z-index: 10;
    // padding: 20px;
`;

function App() {
    const [title, setTitle] = useState('/');
    
    const contentClickHandler = (val) => {
        setTitle(val);
    };

    return (
        <Router>
            <AppContainer>
                <Sidebar getTitle={contentClickHandler} />
                <Content >
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
        </Router>
    );
}

export default App;
