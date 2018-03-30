import React from "react";
import ReactDOM from "react-dom";

import TitleBar from './widget/title-bar';
import InfoPane from './widget/info-pane';
import Img from 'react-image'

import "./less/defaults.less"

import { Link, BrowserRouter, Switch, Route } from 'react-router-dom'

import HomePage from "./page/home"
import SettingsPage from "./page/settings"
import LoginPage from "./page/login"

//<Route component={NoMatch}/>
export default class App extends React.Component {

    render() {

        //var selectedIndex = TitleBar.LINKS.find(item => item[0] === this.props.location.pathname);

        return (

            <BrowserRouter>
                <div className="App">

                    <center>

                        <Switch>
                            <Route path="/" exact component={HomePage}/>
                            <Route path="/login" component={LoginPage}/>
                            <Route path="/settings" component={SettingsPage}/>
                        </Switch>

                    </center>

                </div>
            </BrowserRouter>
        );
    }
};

ReactDOM.render(
    <App/>,
    document.querySelector("#container")
);  