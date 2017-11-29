import pyrogue as pr
import surf

LINK_SPEED_TABLE = {
    '3.125' : {
        'CPLL_CFG0'      : '0x21F8',
        'CPLL_CFG2'      : '0x0004',
        'CPLL_FBDIV'     : '5',
        'PMA_RSV1'       : '0xE000',
        'RXCDR_CFG2': '0x0756',
        'RXCDR_CFG2_GEN3': '0x07E6',        
        'RXOUT_DIV'      : '2',
        'TXOUT_DIV'      : '2',
        'TX_PROGDIV_CFG' : '20.0',
        'CLK_COR_MIN_LAT' : '18',
        'CLK_COR_MAX_LAT' : '21',
        'CLK_COR_SEQ_1_1' : '0b0110111100',
        'CLK_COR_SEQ_1_2' : '0b0100011100',
        'CLK_COR_SEQ_1_3' : '0b0100011100',
        'CLK_COR_SEQ_1_4' : '0b0100011100',        
    },
    '2.5' : {
        'CPLL_CFG0'      : '0x67F8',
        'CPLL_CFG2'      : '0x0007',
        'CPLL_FBDIV'     : '4',
        'PMA_RSV1'       : '0xF000',
        'RXCDR_CFG2': '0x0756',
        'RXOUT_DIV'      : '2',
        'TXOUT_DIV'      : '2',
        'TX_PROGDIV_CFG' : '20.0',
    },
    '1.25' : {
        'CPLL_CFG0'      : '0x67F8' ,
        'CPLL_CFG2'      : '0x0007' ,
        'CPLL_FBDIV'     : '4',
        'PMA_RSV1'       : '0xF000',
        'RXCDR_CFG2': '0x0746',
        'RXOUT_DIV'      : '4',
        'TXOUT_DIV'      : '4',
        'TX_PROGDIV_CFG' : '40.0',
    },
    '5.0' : {
        'CPLL_CFG0'      : '0x67F8' ,
        'CPLL_CFG2'      : '0x0007' ,
        'CPLL_FBDIV'     : '4',
        'PMA_RSV1'       : '0xF000',
        'RXCDR_CFG2': '0x0766',
        'RXOUT_DIV'      : '1',
        'TXOUT_DIV'      : '1',
        'TX_PROGDIV_CFG' : '10.0',
    },
    '6.125' : {
        'CPLL_CFG0'      : '0x21F8',
        'CPLL_CFG2'      : '0x0004',
        'CPLL_FBDIV'     : '5',
        'PMA_RSV1'       : '0xe000',
        'RXCDR_CFG2': '0x0766',
        'RXOUT_DIV'      : '1',
        'TXOUT_DIV'      : '1',
        'TX_PROGDIV_CFG' : '10.0',
    }
}

class AppPgp2bLane(pr.Device):
    def __init__(self, *,
                 name='AppPgp2bLane',
                 description='',
                 linkRate='3.125',
                 **kwargs):
        super().__init__(name=name, description=description, **kwargs)

        self._linkRate=linkRate

        self.add(surf.protocols.pgp.Pgp2bAxi(offset=0x000))
        self.add(surf.xilinx.Gthe3Channel(offset=0x800))

        self.Gthe3Channel.hideVariables(True)
        for key in LINK_SPEED_TABLE['3.125'].keys():
            self.Gthe3Channel.node(key).hidden = False

        for var in self.Gthe3Channel.find(name='(CLK_COR)'):
            var.hidden = False

        self.Gthe3Channel.RX_DATA_WIDTH.hidden = False
        self.Gthe3Channel.TX_DATA_WIDTH.hidden = False        

        self.add(pr.LinkVariable(
            name='LinkRate',
            disp=list(LINK_SPEED_TABLE.keys()),
            linkedSet=self.setLinkRate,
            linkedGet=lambda: self._linkRate))

    def setLinkRate(self, value):
        self._linkRate = value
        params = LINK_SPEED_TABLE[value]
        for k,v in params.items():
            if isinstance(v, str):
                self.Gthe3Channel.node(k).setDisp(v)
            else:
                self.Gthe3Channel.node(k).set(v)
#       self.Pgp2bAxi.ResetRx()
#       self.Pgp2bAxi.ResetTx()
        self.Pgp2bAxi.ResetGt()
        # Need to reset when done

class AppPgp2bQuad(pr.Device):
    def __init__(self, *,
                 name='AppPgp2bLane',
                 description='',
                 numLinks=4,
                 **kwargs):
        super().__init__(name=name, description=description, **kwargs)

        self.addNodes(
            nodeClass=AppPgp2bLane,
            name='AppPgp2bLane',
            number=numLinks,
            offset=0x000,
            stride=0x1000)
