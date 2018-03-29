import React from 'react';
import PropTypes from 'prop-types';

import './index.less'

import {cls} from "../../util/"

export default class CheckBox extends React.Component {
    displayName: "RadioButton";

  render() {
    return (
        <label
            className={cls(this, "", {
                selected: this.props.selected
            }) + " " + this.props.className}
            style={this.props.style}>
            <input className={cls(this, "default")} type="checkbox"/>
            <span className={cls(this, "button")}>
                <span className={cls(this, "buttonFill")}/>
            </span>
            <div className={cls(this, "text")}>
                {this.props.children}
            </div>
        </label>
    );
  }
}
CheckBox.propTypes = {
    className: PropTypes.string,
    value: PropTypes.string.isRequired,
};
CheckBox.defaultProps = {
    className: "",
}