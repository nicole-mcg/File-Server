import React from 'react';

import './index.less'

import { Link } from 'react-router-dom'

import {cls} from "../../util/"

export default class ClientInfo extends React.Component {
    displayName: "ClientInfo";

    constructor(props) {
        super(props);
        this.state = {
            open: false
        };
    }

    toggleOpen() {
        this.setState({
            open: !this.state.open
        })
    }

    render() {

        var _this = this;
        var toggleOpen = function() {
            _this.toggleOpen();
        }


        var info = this.props.info;
        var content = "";

        //Prepare info

        var time = new Date(info.time*1000);
        var today = new Date();
        var timeString = time.getHours() + ':' + ("0" + time.getMinutes()).substr(-2) + ':' + ("0" + time.getSeconds()).substr(-2);

        if (time.date != today.date) {
             timeString += " " + time.getDate() + " " + time.getMonth() 
        }

        if (info.transferring == null) {
            status = "Idle"
        } else {
            status = "Transferring files\t";
            status += info.transferring.file_name + "\t";

            status += Math.round(info.transfer_progress / info.transferring.file_size * 100)
        }

        //Create jsx

        if (this.state.open) {
            content = (
                <div className={cls(this, "content")}>
                    <div>{"Connected: " + timeString}</div>
                    <div>{"Status: " + status}</div>
                    <div>{"Files Sent: " + info.files_sent}</div>
                    <div>{"Data Sent: " + info.data_sent}</div>
                    <div>{"Files Recieved: " + info.files_recieved}</div>
                    <div>{"Data Recieved: " + info.data_recieved}</div>
                </div>
            )
        }

        return (
            <div className={cls(this)}>
                <div className={cls(this, "header", {open: this.state.open})}>
                    {info.address}
                    <div className={cls(this, "showBtn")} onClick={toggleOpen}>
                        {this.state.open ? "-" : "+"}
                    </div>
                </div>
                {content}
            </div>
        )
        
    }
}