import React from "react";

import ContentSpacer from "../widget/content-spacer";
import SubTitle from '../widget/sub-title';
import InfoPane from '../widget/info-pane';
import Button from '../widget/button';
import TextField from '../widget/text-field';
import ClientInfo from '../widget/client-info';
import Img from 'react-image'

import fetch from 'isomorphic-fetch';

import {cls, constants} from "../util/"

import Cookies from 'universal-cookie';

export default class LoginPage extends React.Component {
    displayName: "LoginPage";

    constructor(props) {
        super(props);
        this.interval = null;
        this.state = {
            error: "",
            isLoaded: false
        };
    }

    login() {
        var name = this.name.state.value
        var password = this.password.state.value

        fetch("/api/login", {
            cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
            credentials: 'same-origin', // include, same-origin, *omit
            method: 'POST', // *GET, POST, PUT, DELETE, etc.
            headers: {'Content-Type':'application/json'},
            body: JSON.stringify({
                "name": name,
                "password": password,
            }),
            mode: 'cors', // no-cors, cors, *same-origin
            redirect: 'follow', // *manual, follow, error
            referrer: 'no-referrer', // *client, no-referrer
        })
        .then(res => res.json())
        .then(
            (result) => {
                if (result.session != null) {
                    const cookies = new Cookies();
                    cookies.set("session", result.session);
                    

                    window.location.href = "/"
                } else {
                    this.setState({
                        error: result.error,
                        isLoaded: true,
                    })
                }
            },
            (error) => {
                this.setState({
                    isLoaded: true,
                    error
                });
            }
        )
    }

    signup(u, e, auth=null) {
        var name = this.name.state.value
        var password = this.password.state.value

        if (!!!name || !!!password) {
            alert("Please enter a username and password to sign up with.");
        } else {
            var data = {
                "name": name,
                "password": password
            };
    
            if (auth != null) {
                data["auth_code"] = auth;
            }
    
            fetch("/api/signup", {
                cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
                credentials: 'same-origin', // include, same-origin, *omit
                method: 'POST', // *GET, POST, PUT, DELETE, etc.
                headers: {'Content-Type':'application/json'},
                body: JSON.stringify(data),
                mode: 'cors', // no-cors, cors, *same-origin
                redirect: 'follow', // *manual, follow, error
                referrer: 'no-referrer', // *client, no-referrer
            })
            .then(res => res.json())
            .then(
                (result) => {
    
                    if (result.needs_auth) {
    
                        auth = prompt("Please enter an authorization code:");
                        if (auth != null) {
                            this.signup(u, e, auth);
                        }
    
    
                    } else if (result.session != null) {
                        const cookies = new Cookies();
                        cookies.set("session", result.session);
    
                        window.location.href = "/"
                    } else {
                        this.setState({
                            error: result.error,
                            isLoaded: true,
                        })
                    }
                },
                (error) => {
                    this.setState({
                        isLoaded: true,
                        error: "Could not connect to server"
                    });
                }
            )
        }
    }

    render() {

        return (
            <div style={{width: "100%", height: "100%"}}>
                <InfoPane title="Login" size="small" style={{
                    height: this.state.error == ""  ? "302px" : "255px",
                    margin: "auto",
                    position: "absolute",
                    top: 0,
                    bottom: 0,
                    left: 0,
                    right: 0,
                }}>
                    <ContentSpacer>
                        <TextField name="Name" ref={(c) => this.name = c}></TextField>
                        <TextField name="Password" password ref={(c) => this.password = c}></TextField>
                        <ContentSpacer size="small">
                            <table style={{width: "100%"}}>
                                <tbody>
                                    <tr style={{textAlign: "center"}}>
                                        <td>
                                            <Button onClick={this.login.bind(this)}>Login</Button>
                                        </td>
                                        <td>
                                            <Button onClick={this.signup.bind(this)}>Signup</Button>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </ContentSpacer>
                        <div style={{textAlign: "center"}}>
                            {this.state.error}
                        </div>
                    </ContentSpacer>
                </InfoPane>
            </div>
        )
        
    }
}