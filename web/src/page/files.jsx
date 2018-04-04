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

    fetchData() {
    }

    componentDidMount() {
    }

    componentWillUnmount() {
    }

    render() {

        return (
            <div>
                <TitleBar selectedIndex={[0]} user={this.props.user}> </TitleBar>
                <InfoPane title="Files" size="large">
                    <FileViewer> </FileViewer>
                </InfoPane>
            </div>
        );
    }
};