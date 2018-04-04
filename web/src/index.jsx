import React from "react";
import ReactDOM from "react-dom";

import InfoPane from './widget/info-pane';
import Img from 'react-image'

import "./less/defaults.less"

import { Link, BrowserRouter, Switch, Route } from 'react-router-dom'

import HomePage from "./page/home"
import SettingsPage from "./page/settings"
import LoginPage from "./page/login"
import FilePage from "./page/files"

import fetch from 'isomorphic-fetch';

//<Route component={NoMatch}/>
export default class App extends React.Component {
     constructor(props) {
        super(props);
        this.state = {
            error: null,
            isLoaded: false,
            user: null
        };
    }

    fetchUser() {
        fetch("/api/user", {
            cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
            credentials: 'same-origin', // include, same-origin, *omit
            method: 'GET', // *GET, POST, PUT, DELETE, etc.
            mode: 'cors', // no-cors, cors, *same-origin
            redirect: 'follow', // *manual, follow, error
            referrer: 'no-referrer', // *client, no-referrer
        })
        .then(res => res.json())
        .then(
            (result) => {

                if (result.needs_auth) {
                    console.log("coult not authenticate")
                    this.setState({
                        isLoaded: true,
                        user: null
                    });
                } else {

                    result.refresh_rate_index = result.refresh_rate;
                    if (result.refresh_rate == 0) {
                        result.refresh_rate = 1000;
                    } else if (result.refresh_rate == 1) {
                        result.refresh_rate = 500;
                    } else if (result.refresh_rate == 2) {
                        result.refresh_rate = 100;
                    }

                    this.setState({
                        isLoaded: true,
                        user: result
                    });
                }
            },
            // Note: it's important to handle errors here
            // instead of a catch() block so that we don't swallow
            // exceptions from actual bugs in components.
            (error) => {
                this.setState({
                    isLoaded: true,
                    error
                });
            }
        )
    }

    componentDidMount() {
        this.fetchUser()
    }

    render() {

        //var selectedIndex = TitleBar.LINKS.find(item => item[0] === this.props.location.pathname);

        return (

            <BrowserRouter>
                <div className="App">

                    <center>

                        <Switch>
                            <Route path="/login" component={LoginPage}/>
                            <Route path="/" exact render={() => (<HomePage user={this.state.user}/>) } />
                            <Route path="/files" render={() => (<FilePage user={this.state.user}/>) }/>
                            <Route path="/settings" render={() => (<SettingsPage user={this.state.user}/>) }/>
                            <Route path="/logout" render={() => window.location.href = "/api/logout"}/>
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