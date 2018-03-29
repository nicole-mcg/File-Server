import React from "react";

import ContentSpacer from "../widget/content-spacer";
import CheckBox from "../widget/check-box"
import RadioButton from "../widget/radio-button";
import AddButton from "../widget/add-button";
import InfoPane from '../widget/info-pane';
import SubTitle from '../widget/sub-title';

import Img from 'react-image'

import {cls, constants} from "../util/"

export default class SettingsPage extends React.Component {
    render() {

        return (
            <div>
                <InfoPane title="Profile Settings" size="large">

                    <SubTitle>I am a:</SubTitle>
                    <ContentSpacer>
                        <RadioButton value="male" group="gender">Man</RadioButton>
                        <RadioButton value="female" group="gender">Woman</RadioButton>
                    </ContentSpacer>

                    <SubTitle>Interested in:</SubTitle>
                    <ContentSpacer>
                        <CheckBox value="men">Men</CheckBox>
                        <CheckBox value="women">Women</CheckBox>
                    </ContentSpacer>

                    <SubTitle>Looking for:</SubTitle>
                    <ContentSpacer>
                        <CheckBox value="friends">Friendship</CheckBox>
                        <CheckBox value="love">Relationship</CheckBox>
                        <CheckBox value="love">Hook-up</CheckBox>
                        <AddButton>Add another</AddButton>
                    </ContentSpacer>

                    <SubTitle>Show me:</SubTitle>
                    <ContentSpacer>
                        <CheckBox value="friends">Men</CheckBox>
                        <CheckBox value="love">Women</CheckBox>
                    </ContentSpacer>
                </InfoPane>
            </div>
        );
    }
};