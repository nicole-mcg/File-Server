import React from 'react';

import './index.less'

import ContentSpacer from "../content-spacer";
import ProgressBar from '../progress-bar';
import Button from '../button';

import { Link } from 'react-router-dom'

import {cls} from "../../util/"


class Directory extends React.Component {
    displayName: "Directory";

    constructor(props) {
        super(props);
        this.interval = null;
        this.state = {
            open: false
        };
    }

    toggleOpen() {
    }

    render() {

        return (
            <div className={cls(this)}>
            </div>
        )
        
    }
}

export default class FileViewer extends React.Component {
    displayName: "FileViewer";

    constructor(props) {
        super(props);
        this.interval = null;
        this.state = {
            error: null,
            isLoaded: false,
            data: null
        };
    }

    fetchDirectory(directory) {
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