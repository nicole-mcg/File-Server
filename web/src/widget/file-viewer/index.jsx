import React from 'react';

import './index.less'

import ContentSpacer from "../content-spacer";
import ProgressBar from '../progress-bar';
import Button from '../button';

import { Link } from 'react-router-dom'

import {cls} from "../../util/"


//Props: data, fetch
class File extends React.Component {
    displayName: "File";

    constructor(props) {
        super(props);
        this.interval = null;
        this.state = {
            open: false
        };
    }

    toggleOpen() {
        var data = this.props.data;
        if (data.snapshots == null) {
            this.props.fetch("./" + data.full_path, data);
        }


        this.setState({
            open: !this.state.open,
        });
    }

    render() {

        var file = this.props.data;
        var isDir = file.type == 1;

        var children = [];
        if (file.snapshots != null) {
            for (var i = 0; i < file.snapshots.length; i++) {
                children.push(
                    <File fetch={this.props.fetch} className={cls(this, "child", {open: this.state.open})} key={i} data={file.snapshots[i]}> </File>
                )
            }
        }

        var arrow = "";
        if (isDir) {
            arrow = this.state.open ? "\u25bc" : "\u25b6";

        }

        return (
            <div className={cls(this) + " " + this.props.className}>
                <div className={cls(this, "arrowColumn")}>
                    <span className={cls(this, "arrow")} onClick={this.toggleOpen.bind(this)}>{arrow}</span>
                </div>
                <div className={cls(this, "nameColumn", {openDir: isDir && this.state.open})}>
                    {file.file_name}
                    {children}
                </div>
            </div>
        )
        
    }
}

//Props: path
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

    //file_data is used to have easy access to the file within the data tree
    fetchDirectory(path, file_data=null, isRoot=false) {
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

                //This 
                if (file_data != null) {
                    file_data.snapshots = result.snapshots;
                    result = this.state.data;
                }

                this.setState({
                    error: null,
                    isLoaded: true,
                    data: result,
                });
                console.log(result)
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
        this.fetchDirectory(this.props.path, null, true)
    }

    componentWillUnmount() {
    }

    render() {

        var contents = ""

        if (this.state.data != null) {
            contents = (
                <File fetch={this.fetchDirectory.bind(this)} data={this.state.data}> </File>
            )
        }

        return (
            <div className={cls(this)}>
                {contents}
            </div>
        )
        
    }
}