import React from 'react';
import PropTypes from 'prop-types';

import Button from '../button/index';

import {cls} from "../../util/"

import './index.less'

export default class InfoPane extends React.Component {
    displayName: "InfoPane";
    
	render() {

        var title = "";
        if (this.props.showTitle) {
            title  = (<div className={cls(this, "title")}>{this.props.title}</div>);
        }

		return (
			<div style={this.props.style}
                className={cls(this, "", {
                    medium: this.props.size == "medium",
                    large: this.props.size == "large"
                })}>
			    {title}
			    <div className={cls(this, "content")}>{this.props.children}</div>
			</div>
		);
	}
}

InfoPane.propTypes = {
    size: PropTypes.oneOf(["small", "medium", "large"]),
    showTitle: PropTypes.bool,
};

InfoPane.defaultProps = {
    size: "medium",
    showTitle: true,
    style: {},
}