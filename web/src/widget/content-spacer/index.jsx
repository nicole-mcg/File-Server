import React from 'react';
import PropTypes from 'prop-types';

import './index.less'

import {cls} from "../../util/"

export default class ContentSpacer extends React.Component {
displayName: "ContentSpacer";
  render() {
    return (
        <div
            className={cls(this, "", {
                medium: this.props.size === "medium",
                large: this.props.size === "large",
            }) + " " + this.props.className}
            style={this.props.style}>
            {this.props.children}
        </div>
    );
  }
}

ContentSpacer.propTypes = {
    className: PropTypes.string,
    size: PropTypes.oneOf(["small", "medium", "large"]),
};

ContentSpacer.defaultProps = {
    className: "",
    size: "medium",
}