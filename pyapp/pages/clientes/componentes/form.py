import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from dash import html, Input, Output, State, callback, no_update
from pyapp.infra.entities.cliente import Cliente
from pyapp.infra.schemas.cliente import ClienteSaveDTO, ClienteMergeDTO
from pyapp.utils.generic_util import ObjectUtil, ErrorValidationModel
from pyapp.pages.clientes.schema.ids import (
    FormComponentADDClienteIds, 
    FormComponentEDITClienteIds,
    EnumTypeForm
)
from pyapp.components.dropdown.form_estado import ComponentDropdownEstado, ComponentDropdownEstadoProps
from pyapp.components.dropdown.form_cidade import ComponentDropdownCidade, ComponentDropdownCidadeProps
from pyapp.components.input.input_mask import ComponentMask, ComponentMaskProps, MaskEnum
from typing import Union

class Form:
    
    ids: Union[FormComponentADDClienteIds, FormComponentEDITClienteIds]

    def __init__(self, ctype=EnumTypeForm) -> None:

        self.current_data_form: Cliente = None
        
        self.type_form = ctype
        
        if ctype.name == EnumTypeForm.ADD.name:
            self.ids = FormComponentADDClienteIds()
        else:
            self.ids = FormComponentEDITClienteIds()
            

        
        self.componentEstado = ComponentDropdownEstado(
            ComponentDropdownEstadoProps(
                aio_id=self.ids.aio_id
            )
        )
        
        self.componentCidade = ComponentDropdownCidade(
            ComponentDropdownCidadeProps(
                estado_id_component=self.componentEstado.ids.component_dropdown,
                multi=False,
                aio_id=self.ids.aio_id
            )
        )
        
        self.componentTelefone = ComponentMask(
            props=ComponentMaskProps(mask=MaskEnum.TELEFONE, aio_id=f'{self.ids.aio_id}'))
        
        self.componentCep = ComponentMask(
            props=ComponentMaskProps(mask=MaskEnum.CEP, aio_id=f'{self.ids.aio_id}'))
        
        self.componentCNPJ = ComponentMask(
            props=ComponentMaskProps(mask=MaskEnum.CNPJ, aio_id=f'{self.ids.aio_id}'))

        self.events()
        

    def layout(self, data=None):

        if data:
            self.current_data_form = data

        
        return dbc.Form([
            dbc.Card(
                [
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Razão Social"),
                            dbc.Input(id=self.ids.input_razao_social,
                                      value=ObjectUtil.getattr_model(self.current_data_form, 'razao_social'))
                        ], width=12, class_name='mb-3'),
                        dbc.Col([
                            dbc.Label("Fantasia"),
                            dbc.Input(id=self.ids.input_fantasia,
                                      value=ObjectUtil.getattr_model(self.current_data_form, 'fantasia'))
                        ], width=12, class_name='mb-3'),
                        dbc.Col([
                            dbc.Label("CNPJ"),
                            self.componentCNPJ.layout(
                                ObjectUtil.getattr_model(self.current_data_form, 'cnpj'))
                        ], width=6, class_name='mb-3'),
                        dbc.Col([
                            dbc.Label("Email"),
                            dbc.Input(id=self.ids.input_email,
                                      value=ObjectUtil.getattr_model(self.current_data_form, 'email'))
                        ], width=6, class_name='mb-3'),
                        dbc.Col([
                            dbc.Label("Telefone"),
                            self.componentTelefone.layout(
                                ObjectUtil.getattr_model(self.current_data_form, 'telefone'))
                        ], width=6, class_name='mb-3'),
                        dbc.Col([
                            dbc.Label("Cep"),
                            self.componentCep.layout(ObjectUtil.getattr_model(self.current_data_form, 'cep'))
                        ], width=6, class_name='mb-3'),
                        dbc.Col([
                            dbc.Label("Logradouro"),
                            dbc.Input(id=self.ids.input_logradouro,
                                      value=ObjectUtil.getattr_model(self.current_data_form, 'logradouro'))
                        ], width=6, class_name='mb-3'),
                        dbc.Col([
                            dbc.Label("Bairro"),
                            dbc.Input(id=self.ids.input_bairro,
                                      value=ObjectUtil.getattr_model(self.current_data_form, 'bairro'))
                        ], width=6, class_name='mb-3'),
                        dbc.Col([
                            dbc.Label("Estado"),
                            self.componentEstado.layout(key_filter=ObjectUtil.getattr_model(
                                self.current_data_form, 'municipio.estado.id'))
                        ], width=6, class_name='mb-3'),
                        dbc.Col([
                            dbc.Label("Cidade"),
                            self.componentCidade.layout(
                                key_filter=ObjectUtil.getattr_model(self.current_data_form, 'municipio.id'))
                        ], width=6, class_name='mb-3'),

                    ]),
                ], body=True),
            dbc.Card(
                [
                    dbc.Row(
                        dbc.Col([
                            dbc.Button('Salvar', color='success', id=self.ids.btn_trigger_submit, n_clicks=0),

                        ], width=12, class_name='mt-2'),
                    ),
                ],
                body=True, class_name='mt-2'),
            html.Br(),
            dbc.Row(dbc.Col(id=self.ids.message), className='mt-12')

        ])

    def events(self):
        
        custom_outpts = [Output(self.ids.message, 'children')]
        
        if self.type_form.name == EnumTypeForm.ADD.name:
            custom_outpts.append(Output(self.ids.parent.store_form_save_data, 'data'))
        else:
            custom_outpts.append(Output(self.ids.parent.store_form_save_change_data, 'data'))
            
        
        @callback(
            custom_outpts,
            Input(self.ids.btn_trigger_submit, 'n_clicks'),
            [
                State(self.ids.input_razao_social, 'value'),
                State(self.ids.input_fantasia, 'value'),
                State(self.componentCNPJ.ids.component_mask, 'value'),
                State(self.ids.input_email, 'value'),
                State(self.componentTelefone.ids.component_mask, 'value'),
                State(self.componentCep.ids.component_mask, 'value'),
                State(self.ids.input_logradouro, 'value'),
                State(self.ids.input_bairro, 'value'),
                State(self.componentCidade.ids.component_dropdown, 'value')
            ]
        )
        def form_submit(btn_submit, *args):
            if not btn_submit:
                raise PreventUpdate
            
            try:
                (
                    razao_social,
                    fantasia,
                    cnpj,
                    email,
                    telefone,
                    cep,
                    logradouro,
                    bairro,
                    municipio_id
                ) = args
                
                
                
                save_dto = ClienteSaveDTO(
                    razao_social=razao_social,
                    fantasia=fantasia,
                    cnpj=cnpj,
                    email=email,
                    telefone=telefone,
                    cep=cep,
                    logradouro=logradouro,
                    municipio_id=municipio_id,
                    bairro=bairro
                )


                if self.current_data_form and (self.current_data_form.id):

                    merge_dto = ClienteMergeDTO(
                        **dict(**save_dto.dict(), **dict(id=self.current_data_form.id)))

                    Cliente.update(data=merge_dto)

                    message = 'alterado'

                else:
                    Cliente.save(data=save_dto)
                    message = 'salvo'
                    
                return dbc.Alert(f'Cliente {message} com sucesso!', color='success', duration=3000), True
            except Exception as ex:
                message = ErrorValidationModel.message(ex)
                return dbc.Alert(message, color='danger', duration=5000), no_update