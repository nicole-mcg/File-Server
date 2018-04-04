import React from "react";

import ContentSpacer from "../widget/content-spacer";
import InfoPane from '../widget/info-pane';
import ClientInfo from '../widget/client-info';
import Img from 'react-image'
import TitleBar from '../widget/title-bar';
import FileViewer from '../widget/file-viewer';

import fetch from 'isomorphic-fetch';

import {cls, constants} from "../util/"

export default class FilePage extends React.Component {

    constructor(props) {
        super(props);
        this.interval = null;
        this.state = {
            error: null,
            isLoaded: false,
            clients: []
        };
    }

    fetchData(path) {
        fetch("/api/directorycontents", {
            cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
            credentials: 'same-origin', // include, same-origin, *omit
            method: 'POST', // *GET, POST, PUT, DELETE, etc.
            headers: {'Content-Type':'application/json'},
            body: JSON.stringify({
                "path": path
            }),
            mode: 'cors', // no-cors, cors, *same-origin
            redirect: 'follow', // *manual, follow, error
            referrer: 'no-referrer', // *client, no-referrer
        })
        .then(res => res.json())
        .then(
            (result) => {
                console.log(result)
                alert("Worked")
            },
            (error) => {
                this.setState({
                    isLoaded: true,
                    error
                });
            }
        )
    }

    componentDidMount() {
        this.fetchData(".")
    }

    componentWillUnmount() {
    }

    render() {

        return (
            <div>
                <TitleBar selectedIndex={[0]} user={this.props.user}> </TitleBar>
                <InfoPane title="Files" size="large">
                    <FileViewer>
                        
                    </FileViewer>
                </InfoPane>
            </div>
        );
    }
};