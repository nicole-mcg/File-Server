import React from 'react';
import PropTypes from 'prop-types';

import './index.less'

import {cls} from "../../util/"

export default class RadioButton extends React.Component {
    displayName: "RadioButton";

  render() {
    return (
        <label
            className={cls(this, "") + " " + this.props.className}
            style={this.props.style}>
            <input className={cls(this, "default")} type="radio" name={this.props.group} value={this.props.value} />
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

RadioButton.propTypes = {
    className: PropTypes.string,
    group: PropTypes.string,
    value: PropTypes.string.isRequired,
};

RadioButton.defaultProps = {
    className: "",
    group: "default",
}