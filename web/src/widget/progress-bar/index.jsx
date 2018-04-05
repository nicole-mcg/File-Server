import React from 'react';
import PropTypes from 'prop-types';

import './index.less'

import { Link } from 'react-router-dom'

import {cls} from "../../util/"

export default class ProgressBar extends React.Component {
    displayName: "ProgressBar";

    render() {
        var progress = this.props.progress;

        return (
            <div className={cls(this)}>
                <div className={cls(this, "text")}>
                    {progress + "%"}
                </div>
                <div className={cls(this, "fill")} style={{width: progress + "%"}}>
                    
                </div>
            </div>
        )
        
    }
}
ProgressBar.propTypes = {
    progress: PropTypes.number
}
ProgressBar.defaultProps = {
    progress: 0
}