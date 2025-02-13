#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QGroupBox, QVBoxLayout,\
    QProgressBar, QLineEdit, QComboBox, QLabel, QFormLayout, QDoubleSpinBox, QTableWidget, \
    QTableWidgetItem, QAbstractItemView, QHeaderView, QCheckBox
from PyQt5.Qt import QIcon


class TabRewards_gui(QWidget):
    def __init__(self, imgDir, *args, **kwargs):
        QWidget.__init__(self)
        self.imgDir = imgDir
        self.initRewardsForm()
        mainVertical = QVBoxLayout()
        mainVertical.addWidget(self.rewardsForm)
        buttonbox = QHBoxLayout()
        buttonbox.addStretch(1)
        buttonbox.addWidget(self.btn_Cancel)
        mainVertical.addLayout(buttonbox)
        self.setLayout(mainVertical)



    def initRewardsForm(self):
        self.collateralHidden = True
        self.rewardsForm = QGroupBox()
        self.rewardsForm.setTitle("Transfer Rewards")
        layout = QFormLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(13)
        layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        ##--- ROW 1
        hBox = QHBoxLayout()
        self.mnSelect = QComboBox()
        self.mnSelect.setToolTip("Select Masternode")
        hBox.addWidget(self.mnSelect)
        self.btn_ReloadUTXOs = QPushButton()
        self.btn_ReloadUTXOs.setToolTip("Reload UTXOs")
        refresh_icon = QIcon(os.path.join(self.imgDir, 'icon_refresh.png'))
        self.btn_ReloadUTXOs.setIcon(refresh_icon)
        hBox.addWidget(self.btn_ReloadUTXOs)
        hBox.addStretch(1)
        label = QLabel("Total Address Balance")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        hBox.addWidget(label)
        self.addrAvailLine = QLabel()
        self.addrAvailLine.setToolTip("PIVX Address total balance")
        self.addrAvailLine.setText("--")
        hBox.addWidget(self.addrAvailLine)
        self.btn_toggleCollateral = QPushButton("Show Collateral")
        hBox.addWidget(self.btn_toggleCollateral)
        layout.addRow(QLabel("Masternode"), hBox)
        ## --- ROW 2: REWARDS
        self.rewardsList = QVBoxLayout()
        self.rewardsList.statusLabel = QLabel()
        self.rewardsList.statusLabel.setMinimumWidth(116)
        self.resetStatusLabel('<b style="color:red">Reload Rewards</b>')
        self.rewardsList.addWidget(self.rewardsList.statusLabel)
        self.rewardsList.box = QTableWidget()
        self.rewardsList.box.setMinimumHeight(140)
        #self.rewardsList.box.setMaximumHeight(140)
        self.rewardsList.box.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.rewardsList.box.setSelectionMode(QAbstractItemView.MultiSelection)
        self.rewardsList.box.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.rewardsList.box.setShowGrid(True)
        self.rewardsList.box.setColumnCount(4)
        self.rewardsList.box.setRowCount(0)
        self.rewardsList.box.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.rewardsList.box.verticalHeader().hide()
        item = QTableWidgetItem()
        item.setText("PIVs")
        item.setTextAlignment(Qt.AlignCenter)
        self.rewardsList.box.setHorizontalHeaderItem(0, item)
        item = QTableWidgetItem()
        item.setText("Confirmations")
        item.setTextAlignment(Qt.AlignCenter)
        self.rewardsList.box.setHorizontalHeaderItem(1, item)
        item = QTableWidgetItem()
        item.setText("TX Hash")
        item.setTextAlignment(Qt.AlignCenter)
        self.rewardsList.box.setHorizontalHeaderItem(2, item)
        item = QTableWidgetItem()
        item.setText("TX Output N")
        item.setTextAlignment(Qt.AlignCenter)
        self.rewardsList.box.setHorizontalHeaderItem(3, item)
        item = QTableWidgetItem()
        self.rewardsList.addWidget(self.rewardsList.box)
        layout.addRow(self.rewardsList)
        ##--- ROW 3
        hBox2 = QHBoxLayout()
        self.btn_selectAllRewards = QPushButton("Select All")
        self.btn_selectAllRewards.setToolTip("Select all available UTXOs")
        hBox2.addWidget(self.btn_selectAllRewards)
        self.btn_deselectAllRewards = QPushButton("Deselect all")
        self.btn_deselectAllRewards.setToolTip("Deselect current selection")
        hBox2.addWidget(self.btn_deselectAllRewards)
        hBox2.addWidget(QLabel("Selected rewards"))
        self.selectedRewardsLine = QLabel()
        self.selectedRewardsLine.setMinimumWidth(200)
        self.selectedRewardsLine.setStyleSheet("color: purple")
        self.selectedRewardsLine.setToolTip("PIVX to move away")
        hBox2.addWidget(self.selectedRewardsLine)
        hBox2.addStretch(1)
        self.swiftxCheck = QCheckBox()
        self.swiftxCheck.setToolTip("check for SwiftX instant transaction (flat fee rate of 0.01 PIV)")
        hBox2.addWidget(QLabel("Use SwiftX"))
        hBox2.addWidget(self.swiftxCheck)
        layout.addRow(hBox2)
        ##--- ROW 4
        hBox3 = QHBoxLayout()
        self.destinationLine = QLineEdit()
        self.destinationLine.setToolTip("PIVX address to transfer rewards to")
        hBox3.addWidget(self.destinationLine)
        hBox3.addWidget(QLabel("Fee"))
        self.feeLine = QDoubleSpinBox()
        self.feeLine.setDecimals(8)
        self.feeLine.setPrefix("PIV  ")
        self.feeLine.setToolTip("Insert a small fee amount")
        self.feeLine.setFixedWidth(150)
        self.feeLine.setSingleStep(0.001)
        hBox3.addWidget(self.feeLine)
        self.btn_sendRewards = QPushButton("Send")
        hBox3.addWidget(self.btn_sendRewards)
        layout.addRow(QLabel("Destination Address"), hBox3)
        ##--- ROW 5
        hBox4 = QHBoxLayout()
        hBox4.addStretch(1)
        self.loadingLine = QLabel("<b style='color:red'>Preparing TX.</b> Completed: ")
        self.loadingLinePercent = QProgressBar()
        self.loadingLinePercent.setMaximumWidth(200)
        self.loadingLinePercent.setMaximumHeight(10)
        self.loadingLinePercent.setRange(0, 100)
        hBox4.addWidget(self.loadingLine)
        hBox4.addWidget(self.loadingLinePercent)
        self.loadingLine.hide()
        self.loadingLinePercent.hide()
        layout.addRow(hBox4)
        #--- Set Layout
        self.rewardsForm.setLayout(layout)
        #--- ROW 5
        self.btn_Cancel = QPushButton("Clear/Reload")



    def resetStatusLabel(self, message=None):
        if message is None:
            self.rewardsList.statusLabel.setText('<em><b style="color:purple">Checking explorer...</b></em>')
        else:
            self.rewardsList.statusLabel.setText(message)
        self.rewardsList.statusLabel.setVisible(True)

