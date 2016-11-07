
/**
 * Created by zhangfujun on 9/22/16.
 */
var React = require('react')
var TodoItem = React.createClass({
    render: function(){
        var t = this.props.todo;
        var updateButton;
        if(t.status == 0){
            updateButton = <button onClick={this.handleUpdate && this.handleUpdate.bind(this,t.id,1)} className="btn btn-primary">Done</button>
        }else{
            updateButton = <button onClick={this.handleUpdate && this.handleUpdate.bind(this,t.id,0)}  className="btn btn-danger">UnDone</button>
        }
        return (
            <tr>
                <td>{t.pagename}</td>
                <td>{t.author == 0 ?'未完成' : '已完成'}</td>
                <td>{t.chinese}</td>
                <td>
                    {updateButton}
                    <button className="btn btn-danger" >Delete</button>
                </td>
            </tr>
        )
    }

});
module.exports = TodoItem;