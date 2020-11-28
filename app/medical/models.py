# models.py
from medical import db


class Hostpital(db.Model):

    __tablename__ = 'hospitals'

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(
        db.String(64),
        unique=True,
        index=True,
        server_default=str(uuid4)
    )
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    expire_at = db.Column(db.DateTime, default=datetime.now)
    create_at = db.Column(db.DateTime, default=datetime.now)
    update_at = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, token, user_id, expire_at):
        self.token = token
        self.user_id = user_id
        self.expire_at = expire_at

    @classmethod
    def publish_token(cls, user):
        # パスワード設定用のURLを生成
        token = str(uuid4())
        new_token = cls(
            token,
            user.id,
            datetime.now() + timedelta(days=1)
        )
        db.session.add(new_token)
        return token
    
    @classmethod
    def get_user_id_by_token(cls, token):
        now = datetime.now()
        record = cls.query.filter_by(token=str(token)).filter(cls.expire_at > now).first()
        if record:
            return record.user_id
        else:
            return None
        

    @classmethod
    def delete_token(cls, token):
        cls.query.filter_by(token=str(token)).delete()

class UserConnect(db.Model):

    __tablename__ = 'user_connects'

    id = db.Column(db.Integer, primary_key=True)
    from_user_id = db.Column(
        db.Integer, db.ForeignKey('users.id'), index=True
    ) # どのユーザからの友達申請か
    to_user_id = db.Column(
        db.Integer, db.ForeignKey('users.id'), index=True
    ) # どのユーザへの友達申請か
    status = db.Column(db.Integer, unique=False, default=1)
    # 1 申請中、2が承認済み
    create_at = db.Column(db.DateTime, default=datetime.now)
    update_at = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, from_user_id, to_user_id):
        self.from_user_id = from_user_id
        self.to_user_id = to_user_id

    def create_new_connect(self):
        db.session.add(self)

    @classmethod
    def select_by_from_user_id(cls, from_user_id):
        return cls.query.filter_by(
            from_user_id = from_user_id,
            to_user_id = current_user.get_id()
        ).first()
    
    def update_status(self):
        self.status = 2
        self.update_at = datetime.now()

    @classmethod
    def is_friend(cls, to_user_id):
        user = cls.query.filter(
            or_(
                and_(
                    UserConnect.from_user_id == current_user.get_id(),
                    UserConnect.to_user_id == to_user_id,
                    UserConnect.status == 2
                ),
                and_(
                    UserConnect.from_user_id == to_user_id,
                    UserConnect.to_user_id == current_user.get_id(),
                    UserConnect.status == 2
                )
            )
        ).first()
        return True if user else False

class Message(db.Model):

    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    from_user_id = db.Column(
        db.Integer, db.ForeignKey('users.id'), index=True
    )
    to_user_id = db.Column(
        db.Integer, db.ForeignKey('users.id'), index=True
    )
    is_read = db.Column(
        db.Boolean, default=False
    )
    # 既読のものを確認したか
    is_checked = db.Column(
        db.Boolean, default=False
    )
    message = db.Column(
        db.Text
    )
    create_at = db.Column(db.DateTime, default=datetime.now)
    update_at = db.Column(db.DateTime, default=datetime.now)
    
    def __init__(self, from_user_id, to_user_id, message):
        self.from_user_id = from_user_id
        self.to_user_id = to_user_id
        self.message = message

    def create_message(self):
        db.session.add(self)
    
    @classmethod
    def get_friend_messages(cls, id1, id2, offset_value=0, limit_value=100):
        return cls.query.filter(
            or_(
                and_(
                    cls.from_user_id == id1,
                    cls.to_user_id == id2
                ),
                and_(
                    cls.from_user_id == id2,
                    cls.to_user_id == id1
                )
            )
        ).order_by(desc(cls.id)).offset(offset_value).limit(limit_value).all()

    @classmethod
    def update_is_read_by_ids(cls, ids):
        cls.query.filter(cls.id.in_(ids)).update(
            {'is_read': 1},
            synchronize_session='fetch'
        )

    @classmethod
    def update_is_checked_by_ids(cls, ids):
        cls.query.filter(cls.id.in_(ids)).update(
            {'is_checked': 1},
            synchronize_session='fetch'
        )

    @classmethod
    def select_not_read_messages(cls, from_user_id, to_user_id):
        return cls.query.filter(
            and_(
                cls.from_user_id == from_user_id,
                cls.to_user_id == to_user_id,
                cls.is_read == 0
            )
        ).order_by(cls.id).all()
    
    @classmethod
    def select_not_checked_messages(cls, from_user_id, to_user_id):
        return cls.query.filter(
            and_(
                cls.from_user_id == from_user_id,
                cls.to_user_id == to_user_id,
                cls.is_read == 1,
                cls.is_checked == 0
            )
        ).order_by(cls.id).all()
