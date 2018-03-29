import React from 'react';
import PropTypes from 'prop-types';

import './index.less'

import {cls} from "../../util/"

export default class Button extends React.Component {
displayName: "Button";
  render() {
    return (
        <div
            className={cls(this, "", {
                selected: this.props.selected
            }) + " " + this.props.className}
            style={this.props.style}
            onClick={this.props.onClick}>
            {this.props.children}
        </div>
    );
  }
}


Button.propTypes = {
    className: PropTypes.string,
    selected: PropTypes.bool,
};

Button.defaultProps = {
    className: "",
    selected: false,
}