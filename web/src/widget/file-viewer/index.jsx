import React from 'react';

import './index.less'

import ContentSpacer from "../content-spacer";
import ProgressBar from '../progress-bar';
import Button from '../button';

import { Link } from 'react-router-dom'

import {cls} from "../../util/"

export default class FileViewer extends React.Component {
    displayName: "FileViewer";

    constructor(props) {
        super(props);
        this.interval = null;
        this.state = {
            error: null,
            isLoaded: false,
            client: null
        };
    }

    toggleOpen() {
    }

    fetchData() {
    }

    componentWillUnmount() {
    }

    render() {

        return (
            <div className={cls(this)}>
            </div>
        )
        
    }
}