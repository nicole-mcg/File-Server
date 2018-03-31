import React from "react";

import ContentSpacer from "../widget/content-spacer";
import CheckBox from "../widget/check-box"
import RadioButton from "../widget/radio-button";
import AddButton from "../widget/add-button";
import InfoPane from '../widget/info-pane';
import SubTitle from '../widget/sub-title';
import TitleBar from '../widget/title-bar';
import Button from '../widget/button';
import DropdownMenu from '../widget/dropdown-menu'

import Img from 'react-image'

import {cls, constants} from "../util/"

export default class SettingsPage extends React.Component {

    constructor(props) {
        super(props);
        this.interval = null;
        this.state = {
            auth: ""
        };
    }

    createAuth() {
        fetch("/api/createauth", {
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
                this.setState({
                    auth: result.new_auth
                })
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

    changeSettings(setting, value) {
        var contents = {}
        contents[setting] = value;

        fetch("/api/updatesettings", {
            cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
            credentials: 'same-origin', // include, same-origin, *omit
            method: 'POST', // *GET, POST, PUT, DELETE, etc.
            headers: {'Content-Type':'application/json'},
            body: JSON.stringify(contents),
            mode: 'cors', // no-cors, cors, *same-origin
            redirect: 'follow', // *manual, follow, error
            referrer: 'no-referrer', // *client, no-referrer
        })
        .then(res => res.json())
        .then(
            (result) => {
                console.log(result)
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

    onRefreshRateChange(value) {
        this.changeSettings("refresh_rate", value);
        this.props.user.refresh_rate_index = value;

        if (value == 0) {
            this.props.user.refresh_rate = 1000;
        } else if (value == 1) {
            this.props.user.refresh_rate = 500;
        } else if (value == 2) {
            this.props.user.refresh_rate = 100;
        }
    }

    render() {

        var auth = ""

        if (this.state.auth != "") {
            auth = (
                <div style={{padding: "0 5px", paddingTop: "10px"}}>
                    {this.state.auth}
                </div>
            )
        }

        var refresh_rate_index = 0

        if (this.props.user != null) {
            refresh_rate_index = this.props.user.refresh_rate_index;
        }

        return (
            <div>

                <TitleBar selectedIndex={[3]} user={this.props.user}> </TitleBar>

                <InfoPane title="Profile Settings" size="large">

                    <SubTitle>Add User</SubTitle>
                    <ContentSpacer>
                        <Button onClick={this.createAuth.bind(this)}>Generate Auth</Button>
                        {auth}
                    </ContentSpacer>

                    <SubTitle>Web Settings</SubTitle>
                    <ContentSpacer>
                        <DropdownMenu selected={refresh_rate_index} onChange={this.onRefreshRateChange.bind(this)} label="Web refresh rate:" items={["1 second", "500ms", "100ms"]}></DropdownMenu>
                    </ContentSpacer>

                    <SubTitle>Test</SubTitle>
                    <ContentSpacer>
                        <RadioButton value="radio" group="gender">radio</RadioButton>
                        <RadioButton value="buttons" group="gender">buttons</RadioButton>
                        <CheckBox value="checkbox">checkbox</CheckBox>
                        <AddButton>Add another</AddButton>
                    </ContentSpacer>
                    
                </InfoPane>
            </div>
        );
    }
};