import React from 'react';
import PropTypes from 'prop-types';

import './index.less'

import ContentSpacer from "../content-spacer";
import ProgressBar from '../progress-bar';
import Button from '../button';

import { Link } from 'react-router-dom'

import {cls} from "../../util/"

export default class ClientInfo extends React.Component {
    displayName: "ClientInfo";

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
        if (this.state.open) {
            clearInterval(this.interval);
            this.interval = null
        } else {
            this.tick(this);
        }

        this.setState({
            open: !this.state.open
        });
    }

    fetchData() {
        this.fetching_data = true;
        fetch("/api/clientinfo/" + this.props.info.id, {
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

                this.fetching_data = false;
                this.setState({
                    isLoaded: true,
                    client: result
                });
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

    tick(self) {

        if (!this.fetching_data) {
            self.fetchData()
        }
        
        if (self.interval == null) {
            self.interval = setInterval((function(self) {         //Self-executing func which takes 'this' as self
                return function() {   //Return a function in the context of 'self'
                    self.tick(self); //Thing you wanted to run as non-window 'this'
                }
            })(self), this.props.user.refresh_rate);
        }
    }

    componentWillUnmount() {
        if (this.state.open) {
            clearInterval(this.interval);
        }
    }

    format_data_size(i) {
        var units = [" bytes", "kb", "MB", "GB", "TB", "PB"]

        var unit_index = 0;
        
        while (i > 1024) {
            i /= 1024;
            unit_index++;
        }

        return i.toFixed(2) + units[unit_index];
    }

    render() {

        var _this = this;
        var toggleOpen = function() {
            _this.toggleOpen();
        }


        var active_info = this.props.info;
        var content = "";

        if (this.state.open && this.state.client != null) {

            var info = this.state.client;

            var time = new Date(info.time*1000);
            var today = new Date();
            var timeString = time.getHours() + ':' + ("0" + time.getMinutes()).substr(-2) + ':' + ("0" + time.getSeconds()).substr(-2);

            if (time.date != today.date) {
                 timeString += " " + time.getDate() + " " + time.getMonth() 
            }

            var progress_bar = ""
            if (info.transferring != null) {

                progress_bar = (
                    <ProgressBar progress={Math.round(info.transfer_progress / info.transferring.file_size * 100)}></ProgressBar>
                )

                progress_bar = (
                    <ContentSpacer style={{paddingBottom: 0}}>
                        <div style={{textAlign: "center"}}>
                            {info.transferring.file_name}
                        </div>
                        {progress_bar}
                        <span style={{visibility: "hidden"}}>Placeholder!</span>
                        <span style={{float: "right"}}>
                            {this.format_data_size(info.transfer_progress) + "/" + this.format_data_size(info.transferring.file_size)}
                            {" (###Mb/s)"}
                        </span>
                    </ContentSpacer>
                )
            }

            content = (
                
                <div className={cls(this, "content")}>
                    <div>{"Connected: " + timeString}</div>
                    <table className={cls(this, "table")}>
                        <tbody>
                            <tr>
                                <td>
                                    <div>{"Files Sent: " + info.files_sent}</div>
                                    <div>{"Data Sent: " + this.format_data_size(info.data_sent)}</div>
                                </td>
                                <td>
                                    <div>{"Files Recieved: " + info.files_recieved}</div>
                                    <div>{"Data Recieved: " + this.format_data_size(info.data_recieved)}</div>
                                </td>
                                <td>
                                    <div>{"Queued Packets: " + info.queued_packets}</div>
                                    <div>{"Events to ignore: " + info.queued_packets}</div>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                    {progress_bar}
                </div>
            )
        }

        return (
            <div className={cls(this)}>
                <div className={cls(this, "header", {open: this.state.open})}>
                    {active_info.name}
                    <span style={{fontSize: "18px"}}>
                        {" (" + active_info.address + ")"}
                    </span>
                    <div className={cls(this, "right")}>
                        {active_info.status == "Idle" ? "" : (<img src="/img/3.svg" width={30} height={30}></img>)}
                        <Button className={cls(this, "showBtn")} onClick={toggleOpen}>
                            {this.state.open ? "-" : "+"}
                        </Button>
                    </div>
                </div>
                {content}
            </div>
        )
        
    }
}
ClientInfo.propTypes = {
    info: PropTypes.object,
    user: PropTypes.object
}
ClientInfo.defaultProps = {
    info: {},
    user: {}
}