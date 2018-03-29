import React from 'react';
import PropTypes from 'prop-types';

import './index.less'

import {cls} from "../../util/"

export default class AddButton extends React.Component {
    displayName: "RadioButton";

  render() {
    return (
        <div
            className={cls(this, "", {
                selected: this.props.selected
            }) + " " + this.props.className}
            style={this.props.style}>
            <div className={cls(this, "button")}>
                <div className={cls(this, "plus")}>+</div>
            </div>
            <div className={cls(this, "text")}>
                {this.props.children}
            </div>
        </div>
    );
  }
}
AddButton.propTypes = {
    className: PropTypes.string,
};
AddButton.defaultProps = {
    className: "",
}